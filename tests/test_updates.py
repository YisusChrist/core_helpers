from _pytest.capture import CaptureResult
import pytest


from core_helpers.updates import check_updates

# List of URLs to test
URLS: list[str] = [
    "https://github.com/vuejs/vue",
    "https://github.com/Jules-WinnfieldX/CyberDropDownloader",
    "https://gitlab.com/TheEvilSkeleton/Upscaler",
    "https://codeberg.org/forgejo/forgejo",
    "https://gitea.com//docker/metadata-action",
    "https://gitea.angry.im/PeterCxy/OpenEUICC",
    "https://gitee.com/LongbowEnterprise/BootstrapBlazor",
    "https://gitee.com/cxasm/notepad--",
]


def run_check_updates_test(
    url: str,
    capsys: pytest.CaptureFixture[str],
    expected_output: str,
    error_expected: bool = False,
) -> None:
    """
    Helper function to test check_updates with various URLs and expected output.

    Args:
        url (str): The URL to check for updates.
        capsys (pytest.CaptureFixture[str]): Pytest fixture to capture stdout/stderr.
        expected_output (str): The expected output or a substring that should be present in the output.
        error_expected (bool): Whether an error message is expected in the output.
    """
    # Call check_updates with the URL and a dummy current_version
    check_updates(url, "0.0.1")

    # Capture the output
    captured: CaptureResult[str] = capsys.readouterr()

    # Assert that output is not empty
    assert captured.out, f"No output was printed for URL: {url}"

    # Check for expected error or success message
    if error_expected:
        assert (
            expected_output in captured.out
        ), f"Expected error not found in output for URL: {url}"
    else:
        assert (
            "ERROR" not in captured.out
        ), f"Unexpected error found in output for URL: {url}"


@pytest.mark.parametrize("url", URLS)
def test_check_updates(url: str, capsys: pytest.CaptureFixture[str]) -> None:
    """Test the check_updates function with various URLs."""
    run_check_updates_test(url, capsys, expected_output="", error_expected=False)


def test_no_release(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the check_updates function with a URL that has no releases."""
    run_check_updates_test(
        "https://git.cryto.net/joepie91/box",
        capsys,
        expected_output="ERROR: Could not check for updates. No releases or tags found",
        error_expected=True,
    )


def test_invalid_url(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the check_updates function with an invalid URL."""
    run_check_updates_test(
        "https://example.com",
        capsys,
        expected_output="ERROR: Unsupported platform",
        error_expected=True,
    )
